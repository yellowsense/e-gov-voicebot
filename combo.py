import requests
import json
import base64

def ASR_config_call(language):
    url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    payload = json.dumps({
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": language
                    }
                }
            }
        ],
        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    })
    
    headers = {
        'ulcaApikey': "52f4f12385-ffbb-42f6-87c1-d0735497010d",
        'userID': "ec5a454995804b86a821daea89f8034b",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    json_object = response.json()
    serviceID = json_object['pipelineResponseConfig'][0]['config'][0]['serviceId']
    inference_api_key = json_object['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']

    return serviceID, inference_api_key


def ASR_compute_call(language, audio_64):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    serviceID, infer_key = ASR_config_call(language)

    payload = json.dumps({
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": language
                    },
                    "serviceId": serviceID,
                    "audioFormat": "wav",
                    "samplingRate": 16000
                }
            }
        ],
        "inputData": {
            "audio": [
                {
                    "audioContent": audio_64
                }
            ]
        }
    })
    
    headers = {
        'Authorization': infer_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    json_obj = response.json()
    out_text = json_obj['pipelineResponse'][0]['output'][0]['source']
    return out_text


def transcribe_audio(file_path, language):
    """Main function to transcribe audio from a file."""
    with open(file_path, 'rb') as f:
        audio_bytes = f.read()
    
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    out = ASR_compute_call(language, base64_audio)
    return out

# Example usage:
if __name__ == "__main__":
    lan = 'ml'
    transcription = transcribe_audio('recording.wav', lan)
    # print(transcription)
    # return transcription
