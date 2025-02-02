#include "ZoomSDKAudioRawDataDelegate.h"
#include "meeting_service_components/meeting_participants_ctrl_interface.h"
#include "meeting_service_interface.h"

#include <iostream>
#include <sstream>
#include <fstream>
#include <iomanip> // For std::put_time
#include <chrono> // For time handling

ZoomSDKAudioRawDataDelegate::ZoomSDKAudioRawDataDelegate(bool useMixedAudio, IMeetingService* meetingService)
    : m_useMixedAudio(useMixedAudio), m_meetingService(meetingService), m_recordingStarted(false), m_currentNodeId(0) {}

void ZoomSDKAudioRawDataDelegate::onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) {
    std::stringstream path;
    path << m_dir << "/node-" << node_id << ".pcm";
    writeToFile(path.str(), data);

    std::cout << "[DEBUG] onOneWayAudioRawDataReceived called" << std::endl;
    std::cout << "[DEBUG] Node ID: " << node_id << std::endl;

    IUserInfo* userInfo = getUserInfoByNodeId(node_id);
    if (userInfo) {
        std::string userName = userInfo->GetUserName();
        bool isH323User = userInfo->IsH323User();

        if (isH323User) {
            auto now = std::chrono::system_clock::now();

            if (!m_recordingStarted) {
                m_startTime = now;
                m_speakerStartTimes[node_id] = m_startTime;
                
                auto start = std::chrono::system_clock::to_time_t(m_startTime);
                std::cout << "Recording started, Initial Start_Time: " << std::put_time(std::localtime(&start), "%Y-%m-%d %H:%M:%S") << std::endl;

                m_currentSpeaker = userName;
                m_recordingStarted = true;
                m_currentNodeId = node_id;
            } else if (node_id != m_currentNodeId || m_currentSpeaker != userName) {
                logSpeakerChange(node_id, userName);
                m_currentNodeId = node_id;
                m_currentSpeaker = userName;
                m_startTime = now;
                m_speakerStartTimes[node_id] = m_startTime;
            }
        }
    } else {
        std::cout << "User Info not found for Node ID: " << node_id << std::endl;
    }
}

void ZoomSDKAudioRawDataDelegate::logSpeakerChange(uint32_t node_id, const std::string& newSpeaker) {
    if (!m_currentSpeaker.empty() && m_speakerStartTimes.find(m_currentNodeId) != m_speakerStartTimes.end()) {
        auto end_time = std::chrono::system_clock::now();
        auto start_time_t = std::chrono::system_clock::to_time_t(m_speakerStartTimes[m_currentNodeId]);
        auto end_time_t = std::chrono::system_clock::to_time_t(end_time);

        // Log only if the speaker has actually changed
        if (m_currentSpeaker != newSpeaker) {
            std::cout << "UserName: " << m_currentSpeaker 
                      << ", Start_Time: " << std::put_time(std::localtime(&start_time_t), "%Y-%m-%d %H:%M:%S") 
                      << ", End_Time: " << std::put_time(std::localtime(&end_time_t), "%Y-%m-%d %H:%M:%S") 
                      << std::endl;

            logSpeakerChangeToFile(m_currentSpeaker, start_time_t, end_time_t);

            // Update the start time for the new speaker
            m_speakerStartTimes[node_id] = end_time;
        }
    }
}

void ZoomSDKAudioRawDataDelegate::logSpeakerChangeToFile(const std::string& speaker, std::time_t start_time, std::time_t end_time) {
    std::size_t dot = m_filename.find_last_of('.');

    // Extract the part of the filename before the dot
    std::string path_file = m_filename.substr(0, dot);

    // Open the file for appending
    std::ofstream file(path_file + ".txt", std::ios::app);

    if (file.is_open()) {
        file << "UserName: " << speaker 
             << ", Start_Time: " << std::put_time(std::localtime(&start_time), "%Y-%m-%d %H:%M:%S")
             << ", End_Time: " << std::put_time(std::localtime(&end_time), "%Y-%m-%d %H:%M:%S")
             << std::endl;
        file.close();
    } else {
        std::cout << "[ERROR] Failed to open log file." << std::endl;
    }
}

ZOOMSDK::IUserInfo* ZoomSDKAudioRawDataDelegate::getUserInfoByNodeId(uint32_t nodeId) {
    IMeetingParticipantsController* participantsController = m_meetingService->GetMeetingParticipantsController();
    return participantsController ? participantsController->GetUserByUserID(nodeId) : nullptr;
}

void ZoomSDKAudioRawDataDelegate::onShareAudioRawDataReceived(AudioRawData* data) {
    std::stringstream ss;
    ss << "Shared Audio Raw data: " << data->GetBufferLen() << "b at " << data->GetSampleRate() << "Hz";
    Log::info(ss.str());
}

void ZoomSDKAudioRawDataDelegate::writeToFile(const std::string& path, AudioRawData* data) {
    std::ofstream file(path, std::ios::out | std::ios::binary | std::ios::app);

    if (!file.is_open()) {
        std::cerr << "Failed to open audio file path: " << path << std::endl;
        return;
    }

    file.write(data->GetBuffer(), data->GetBufferLen());
    file.flush();
    file.close();

    std::stringstream ss;
    ss << "Writing " << data->GetBufferLen() << "b to " << path << " at " << data->GetSampleRate() << "Hz";
    std::cout << "[DEBUG] " << ss.str() << std::endl;
}

void ZoomSDKAudioRawDataDelegate::onMixedAudioRawDataReceived(AudioRawData* data, uint32_t node_id) {
    if (!m_useMixedAudio) return;

    if (m_dir.empty()) {
        std::cerr << "Output Directory cannot be blank" << std::endl;
        return;
    }

    if (m_filename.empty())
        m_filename = "test.pcm";

    std::stringstream path;
    path << m_dir << "/" << m_filename;

    std::cout << "[DEBUG] onMixedAudioRawDataReceived called" << std::endl;
    std::cout << "[DEBUG] Node ID: " << node_id << std::endl;

    writeToFile(path.str(), data);
}

void ZoomSDKAudioRawDataDelegate::setDir(const std::string& dir) {
    m_dir = dir;
}

void ZoomSDKAudioRawDataDelegate::setFilename(const std::string& filename) {
    m_filename = filename;
}

void ZoomSDKAudioRawDataDelegate::onOneWayInterpreterAudioRawDataReceived(AudioRawData* data, const zchar_t* pLanguageName) {
    // Implementation here
}
