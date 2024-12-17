from postman 

hit the post api 

http://127.0.0.1:8000/api/extract_relations/

request body 
------------

{"text": "ZmXLG3b (GRMZM2G429113, rank 1), encoding a guanine nucleotide-binding protein predicted to be involved in the response to desiccation"}

response
---------

{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "Subject = ZmXLG3b (GRMZM2G429113, rank 1)\nobject = a guanine nucleotide-binding protein\nrelation = encoding\n\nSubject = a guanine nucleotide-binding protein\nobject = the response to desiccation\nrelation = involved in\n"
                    }
                ],
                "role": "model"
            },
            "finishReason": "STOP",
            "avgLogprobs": -0.04057646566821683
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 240,
        "candidatesTokenCount": 62,
        "totalTokenCount": 302
    },
    "modelVersion": "gemini-1.5-flash-latest"
}

