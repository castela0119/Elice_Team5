import re
import traceback
import typing as ty

import pytube
from backend.apps.ai.hanspell import spell_checker
from krwordrank.word import summarize_with_keywords
from youtube_transcript_api import YouTubeTranscriptApi

sample_url = "https://www.youtube.com/watch?v=mc02IZhouEg"
sample_url2 = "https://youtu.be/mc02IZhouEg"


class YoutubeInference:
    youtube_id_compiler = re.compile("(v=)([a-zA-Z0-9-_]{11})")
    stop_words_path = "backend/apps/ai/stopwords.txt"
    youtube_url_prefix = "https://www.youtube.com/watch?v="

    with open(stop_words_path, "r", encoding="utf-8") as fp:
        stop_words = fp.readline().strip().split()

    # hyper parmas
    beta = 0.85  # PageRank의 decaying factor beta
    max_iter = 10
    min_count = 2  # 단어의 최소 출현 빈도수 (그래프 생성 시)
    max_length = 10  # 단어의 최대 길이
    verbose = True

    def __init__(self, slug: str = sample_url2[17:]):
        self._url = self.youtube_url_prefix + slug
        yt = pytube.YouTube(self._url)
        self._title = yt.title
        self._thumbnail = yt.thumbnail_url
        self._author = yt.author

    @property
    def url(self) -> str:
        return self._url

    @property
    def thumbnail_url(self) -> str:
        return self._thumbnail

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    def inference(self) -> ty.List[dict]:
        try:
            scripts_info = self.get_transcript()  # {00:01: {"script":"가나다라마바사"}} 형식

            sorted_scripts_N_time = sorted(scripts_info.items())
            scripts = [
                value["script"] for key, value in sorted_scripts_N_time
            ]  # 시간 순으로 정렬된 스크립트
            # timestamps = [key for key, value in sorted_scripts_N_time]

            word_importance = self.get_script_keywords(scripts)  # 무슨 단어가 몇 점인지

            # keywords = list(word_importance.keys())

            scripts_info, keywords_info, words_freq = self.get_script_importance(
                scripts_info, word_importance
            )
            return scripts_info, keywords_info, words_freq
        except Exception:
            traceback.print_exc()
            return None

    def get_transcript(self, lang: str = "ko") -> ty.Dict[str, dict]:
        youtube_id: str = self.gen_youtube_id(self.url)
        scripts: dict = YouTubeTranscriptApi.get_transcript(
            youtube_id, languages={lang}
        )

        rets = {}
        for script in scripts:
            time_str = self.time_int_to_str(script["start"])
            processed_script = self.preprocessing(script["text"])
            rets[time_str] = {"script": processed_script, "importance": 0}
        return rets

    def get_script_keywords(self, scripts):
        keywords = summarize_with_keywords(
            texts=scripts,
            min_count=self.min_count,
            max_length=self.max_length,
            beta=self.beta,
            max_iter=self.max_iter,
            stopwords=self.stop_words,
            verbose=self.verbose,
        )

        words = []
        word_importance = {}
        for word, importance in sorted(
            keywords.items(), key=lambda x: x[1], reverse=True
        ):
            # print('%8s:\t%.4f' % (word, r))
            words.append(word)

        for word, importance in sorted(
            keywords.items(), key=lambda x: x[1], reverse=True
        )[:20]:
            # print('%8s:\t%.4f' % (word, r))
            # freq_words.append(word)
            word_importance[word] = importance
        return word_importance

    def get_script_importance(self, scripts_info, word_importance):
        keywords_info = {}
        words_freq = {}
        idx = 0
        for timestamp in scripts_info:
            cnt = 0
            for word in list(word_importance.keys()):
                if words_freq.get(word) is None:
                    words_freq[word] = scripts_info[timestamp]["script"].count(word)
                else:
                    words_freq[word] += scripts_info[timestamp]["script"].count(word)
                if word in scripts_info[timestamp]["script"]:
                    cnt += 1

                    keywords_info[idx] = {
                        "keyword": word,
                        "timestamp": timestamp,
                        "score": word_importance[word],
                    }
                    idx += 1

            scripts_info[timestamp]["importance"] = cnt

        return scripts_info, keywords_info, words_freq

    def gen_youtube_id(self, url):
        return self.youtube_id_compiler.search(url).group(2)

    def time_int_to_str(self, start_time):
        minute = str(int(start_time) // 60)
        second = str(int(start_time) - int(minute) * 60)
        if len(minute) == 1 and len(second) == 1:
            # 초와 분 둘 다 한자리 숫자이면
            ret = "0" + minute + ":0" + second
        elif len(minute) == 1:
            # 분이 한자리 숫자이면
            ret = "0" + minute + ":" + second
        elif len(second) == 1:
            # 초가 한자리 숫자이면
            ret = minute + ":0" + second
        else:
            ret = minute + ":" + second
        return "00:" + ret

    def preprocessing(self, script):
        new_script = re.sub("\n", "", script)
        new_script = re.sub("[a-zA-Z]", "", new_script)
        new_script = re.sub("\d+", "", new_script)
        new_script = re.sub("[ㄱ-ㅎㅏ-ㅣ]+", "", new_script)
        new_script = re.sub(
            "[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]", "", new_script
        )
        new_script = spell_checker.check(new_script).checked

        return new_script


# yi = YoutubeInference("O4xuYk20J40")
# scripts_info, keywords_info, words_freq = yi.inference()
# import pprint

# pprint.pprint(scripts_info)
# pprint.pprint(keywords_info)
# pprint.pprint(words_freq)
