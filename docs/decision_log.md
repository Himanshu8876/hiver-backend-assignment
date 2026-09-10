# Decision Log

## 1. Brand selection
Selected AmazonHelp because it has a large number of customer-support interactions in the dataset, providing enough historical examples for retrieval.

## 2. Intent taxonomy
Defined 11 support intents based on recurring issue types observed in the sampled customer messages.

## 3. Golden evaluation size
Used 200 manually labelled examples, which is within the required 150–250 range.

## 4. Fixed evaluation sample
Used a fixed random seed when sampling the golden set so the evaluation can be reproduced.

## 5. Duplicate historical pairs
Retained duplicate customer-to-reply pairs because the same customer message can have multiple historical support responses.

## 6. Retrieval method
Used TF-IDF with cosine similarity as a simple, interpretable first retrieval approach.

## 7. Retrieval depth
Retrieved the top 3 historical examples so the reply generator has multiple pieces of evidence.

## 8. Escalation threshold
Escalate when the top historical similarity is below 0.30 because low similarity means the system has weak historical evidence.

## 9. Sensitive issue handling
Payment, account/security, and refund/return issues are treated conservatively because they may require account-specific investigation.

## 10. Trivial baseline
Used the majority-class classifier as a trivial baseline to establish a minimum reference point.

## 11. Keyword baseline
Built a simple keyword classifier as a stronger but still interpretable baseline.

## 12. Gemini evaluation reporting
Did not report the fallback-heavy Gemini evaluation as genuine Gemini performance because API quota exhaustion caused fallback predictions.

## 13. LLM judge reporting
Did not report LLM-judge quality scores because all 10 judge requests failed due to API quota exhaustion.

## 14. Multilingual limitation
Kept TF-IDF retrieval despite weak multilingual performance because it provides a simple reproducible baseline and exposes an important limitation.

## 15. Separate decision layer
Separated intent classification from the auto-handle/escalate decision so classification confidence and operational risk can be considered independently.