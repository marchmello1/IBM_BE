JOB_TEMPLATE = {
    "elements": [{
        "externalJobPostingId": "external-job-id-0001",
        "title": "Test Job",
        "description": "Lorem Ipsum is simply...",
        "integrationContext": "urn:li:organization:1234",
        "listedAt": 1558045934000,
        "jobPostingOperationType": "CREATE",
        "location": "Enterprise, UT",
        "availability": "PUBLIC",
        "industries": ["urn:li:industry:3"],
        "categories": ["advr"],
        "trackingPixelUrl": "http://localhost:5000/jobs/tracking",
        "companyApplyUrl": "http://localhost:5000",
        "posterEmail": "test@email.com",
        "onsiteApplyConfiguration": {
            "jobApplicationWebhookUrl": "https://customer-webhook.com/api/webhook",
            "questions": {
                "voluntarySelfIdentificationQuestions": {},
                "educationQuestions": {"educationExperienceQuestionSet": {}},
                "workQuestions": {"workExperienceQuestionSet": {}},
                "additionalQuestions": {
                    "customQuestionSets": [{
                        "repeatLimit": 1,
                        "questions": [{
                            "required": True,
                            "partnerQuestionIdentifier": "question1",
                            "questionText": "Please choose the right answer",
                            "questionDetails": {
                                "multipleChoiceQuestionDetails": {
                                    "choices": [
                                        {"symbolicName": "wrong", "displayValue": "This is the wrong answer"},
                                        {"symbolicName": "right", "displayValue": "This is the correct answer"},
                                        {"symbolicName": "right2", "displayValue": "This is also the correct answer"}
                                    ],
                                    "selectMultiple": False,
                                    "defaultValueSymbolicName": "right",
                                    "preferredFormComponent": "DROPDOWN",
                                    "favorableMultipleChoiceAnswer": {
                                        "favorableSymbolicNames": ["right", "right2"]
                                    }
                                }
                            }
                        }]
                    }]
                }
            }
        }
    }]
}
