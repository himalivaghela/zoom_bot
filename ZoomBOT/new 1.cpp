#include "ZoomSDKAudioRawDataDelegate.h"
#include "meeting_service_components/meeting_participants_ctrl_interface.h"
#include "meeting_service_interface.h"

#include <iostream>
#include <sstream>
#include <fstream>
#include <iomanip> // For std::put_time
#include <chrono>

using namespace std;
using namespace ZOOMSDK;

std::string getCurrentTimestamp(){
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    auto milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%H:%M:%S") << '.' << std::setw(3) << std::setfill('0') << milliseconds.count();
    return ss.str();
}

void ZoomSDKAudioRawDataDelegate::writeToFile(const std::string& path, AudioRawData* data) {
    // Only write data if the speaker is active
    if (!m_currentSpeaker.empty()) {
        std::ofstream file(path, std::ios::out | std::ios::binary | std::ios::app);

        if (!file.is_open()) {
            std::cerr << "[ERROR] Failed to open audio file path: " << path << std::endl;
            return;
        }

        // Write the raw audio data
        file.write(data->GetBuffer(), data->GetBufferLen());
        file.flush();
        file.close();

        // Log the current timestamp
        auto timestamp = getCurrentTimestamp();
        std::cout << "[DEBUG] Writing " << data->GetBufferLen() << " bytes to " << path << " at " << data->GetSampleRate() << " Hz" << std::endl;
        std::cout << "[DEBUG] Timestamp: " << timestamp << std::endl;
    }
}

void ZoomSDKAudioRawDataDelegate::logSpeakerChange(uint32_t node_id, const std::string& newSpeaker) {
    if (!m_currentSpeaker.empty() && m_speakerStartTimes.find(m_currentNodeId) != m_speakerStartTimes.end()) {
        auto end_time = std::chrono::steady_clock::now();
        auto start_time = m_speakerStartTimes[m_currentNodeId];
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

        // Log only if the speaker has actually changed
        if (duration > 0 && m_currentSpeaker != newSpeaker) {
            long long start_time_ms = std::chrono::duration_cast<std::chrono::milliseconds>(start_time.time_since_epoch()).count();
            long long end_time_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end_time.time_since_epoch()).count();

            std::cout << "UserName: " << m_currentSpeaker << ", Start_Time: " << start_time_ms << " ms, End_Time: " << end_time_ms << " ms, Duration: " << duration << " ms" << std::endl;
            logSpeakerChangeToFile(m_currentSpeaker, start_time_ms, end_time_ms);

            m_recordingStarted = false; // Stop recording as the speaker has changed
        }
    }

    // Start recording for the new speaker
    m_speakerStartTimes[node_id] = std::chrono::steady_clock::now();
    m_currentNodeId = node_id;
    m_currentSpeaker = newSpeaker;
    m_recordingStarted = true; // Start recording as there's a new speaker
}

void ZoomSDKAudioRawDataDelegate::logSpeakerChangeToFile(const std::string& speaker, long long start_time, long long end_time) {
    std::size_t dot = m_filename.find_last_of('.');

    // Extract the part of the filename before the dot
    std::string path_file = m_filename.substr(0, dot);

    std::ofstream file(path_file + ".txt", std::ios::app);

    if (file.is_open()) {
        file << "UserName: " << speaker << ", Start_Time: " << start_time << " ms";
        if (end_time >= 0) {
            file << ", End_Time: " << end_time << " ms";
        }
        file << std::endl;
        file.close();
    } else {
        std::cout << "[ERROR] Failed to open log file." << std::endl;
    }
}

void ZoomSDKAudioRawDataDelegate::onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) {
    std::stringstream path;
    path << m_dir << "/node-" << node_id << ".pcm";

    // Write data to file only if recording has started
    if (m_recordingStarted) {
        writeToFile(path.str(), data);
    }

    std::cout << "[DEBUG] onOneWayAudioRawDataReceived called" << std::endl;
    std::cout << "[DEBUG] Node ID: " << node_id << std::endl;

    IUserInfo* userInfo = getUserInfoByNodeId(node_id);
    if (userInfo) {
        std::string userName = userInfo->GetUserName();
        bool isH323User = userInfo->IsH323User();

        if (isH323User) {
            if (!m_recordingStarted) {
                m_speakerStartTimes[node_id] = std::chrono::steady_clock::now();
                m_currentSpeaker = userName;
                m_recordingStarted = true;
                m_currentNodeId = node_id;
                std::cout << "Recording started for user: " << userName << std::endl;
            } else if (node_id != m_currentNodeId || m_currentSpeaker != userName) {
                logSpeakerChange(node_id, userName);
                m_currentNodeId = node_id;
                m_currentSpeaker = userName;
                m_speakerStartTimes[node_id] = std::chrono::steady_clock::now();
            }
        }
    } else {
        std::cout << "User Info not found for Node ID: " << node_id << std::endl;
    }
}
