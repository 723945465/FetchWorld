import OCR_PaddleOCRTools
import TopicKwordsAnalysis
import main_TopicKeywordsAnalysis


def analysis_DWH_image_text(dwh_reletve_path,TopicName):
    return analysis_local_image_text("")


def analysis_local_image_text(local_image_path):

    ocr_res = OCR_PaddleOCRTools.PicToText_PaddleOCR(local_image_path)
    if "##Error##" in ocr_res:
        return ocr_res

    TopicList = main_TopicKeywordsAnalysis.getTopicList()
    for tempTopic in TopicList:
        Topic_keywords_dict_list = TopicKwordsAnalysis.construct_topic_keywords(tempTopic)
        if len(Topic_keywords_dict_list) == 0:
            print("Topic内没有关键词")
            return f"##Error## Topic {tempTopic}内没有关键词"
        match_condition_dict = {}
        match_score = 0
        matched_keyword_list = []
        matched_keyword_list, match_score, match_condition_dict = TopicKwordsAnalysis.analyze_one_article(ocr_res,
                                                                                                          Topic_keywords_dict_list,
                                                                                        tempTopic)
        print(f"res of Topic: {tempTopic}")
        print(match_condition_dict)
        print(match_score)
        print(matched_keyword_list)

    return "success"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    res = analysis_local_image_text("E:\\1.png")
    if "success" not in res:
        print(f"error: {res}")
    # picpath = r"C:\1710483238241.jpg"
    # res = OCR_wx.pic_to_text(picpath)
    # print(res)

