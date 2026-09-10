# Decision Log

## 1. Brand selection: AmazonHelp
Selected AmazonHelp as the target brand because it has a large number of historical support interactions in the Customer Support on Twitter dataset. This provides enough examples for both retrieval and evaluation.

## 2. Intent taxonomy
Defined a small taxonomy of 11 intents based on recurring customer-support themes observed in the dataset. The goal was to keep the taxonomy useful for automation without creating too many fine-grained classes.

## 3. Golden evaluation set size
Created a 200-example hand-labelled golden set. This is within the required 150–250 example range and provides enough examples to compare systems while keeping manual labeling manageable.

## 4. Golden set sampling
Used a fixed random seed when sampling the evaluation examples so that the evaluation set can be reproduced.

## 5. Historical conversation pairing
Used the dataset's response relationships to connect customer messages with AmazonHelp replies. The customer tweet's response_tweet_id was used to identify the corresponding AmazonHelp response.

## 6. Duplicate historical pairs
Kept duplicate customer-to-reply pairs because the same customer message can have multiple historical support responses. Removing them could discard legitimate examples of different resolutions.

## 7. TF-IDF retrieval
Used TF-IDF with cosine similarity as the first retrieval approach. It is simple, fast, interpretable, and provides a strong baseline without requiring a vector database or embedding API.

## 8. Top-3 retrieval
Retrieved the top three historical examples for each customer message. This provides multiple pieces of evidence while keeping the generation prompt reasonably small.

## 9. Historical replies as grounding evidence
Used actual AmazonHelp replies as evidence for response generation. This reduces the risk of generating unsupported policies or resolutions.

## 10. Sensitive-intent escalation
Configured payment, account/security, and refund/return issues to escalate because these cases may require account-specific or transaction-specific investigation.

## 11. Retrieval-confidence escalation
Configured cases with low retrieval similarity to escalate instead of automatically generating a resolution when there is insufficient historical evidence.

## 12. Keyword fallback
Added a deterministic keyword-based fallback for cases where the LLM API is unavailable. This prevents the system from failing completely when the external model cannot be reached.

## 13. Macro F1 reporting
Reported macro F1 in addition to accuracy because the golden set contains uneven numbers of examples across intents. Macro F1 gives each intent equal importance.

## 14. Two baseline systems
Used both a trivial majority-class baseline and a keyword baseline. The trivial baseline establishes a minimum reference point, while the keyword baseline represents a simple non-LLM classifier.

## 15. API quota and reproducibility
The Gemini API was used for the LLM components, but the evaluation also includes deterministic local components. This is important because external API availability and quota limits can affect reproducibility.