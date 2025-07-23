import logging
import requests
from typing import Optional, List, Tuple

from open_webui.env import SRC_LOG_LEVELS
from open_webui.retrieval.models.base_reranker import BaseReranker


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


class ExternalReranker(BaseReranker):
    def __init__(
            self,
            api_key: str,
            url: str = "http://localhost:8080/rerank",
            model: Optional[str] = None,
    ):
        self.api_key = api_key
        self.url = url
        # self.model is not needed for the TEI request payload but we store it in case.
        self.model = model

    def predict(self, sentences: List[Tuple[str, str]]) -> Optional[List[float]]:
        if not sentences:
            return []

        query = sentences[0][0]
        docs = [i[1] for i in sentences]

        payload = {
            "query": query,
            "texts": docs,
            "top_n": len(docs),
        }

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            log.info(f"ExternalReranker:predict:query {query}")
            log.info(f"ExternalReranker:predict:payload {payload}")
            r = requests.post(
                self.url,
                headers=headers,
                json=payload,
            )
            r.raise_for_status()
            data = r.json()

            if isinstance(data, list):
                # The response is a list of dicts: [{"index": 0, "score": 0.9}, {"index": 1, "score": 0.1}]
                sorted_results = sorted(data, key=lambda x: x["index"])
                log.info(sorted_results)
                return [result["score"] for result in sorted_results]
            else:
                log.error(f"Unexpected response format from reranker. Expected a list, got {type(data)}")
                return None

        except Exception as e:
            log.exception(f"Error in external reranking: {e}")
            return None
