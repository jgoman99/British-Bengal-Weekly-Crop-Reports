def async_detect_document():
    # imports
    from google.cloud.vision_v1 import enums
    from google.protobuf.json_format import MessageToJson
    import json

    # Set up Vision API
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    features = [{"type": enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
    mime_type = 'application/pdf'

    # from GCP
    gcs_source_uri = "gs://cloud-samples-data/vision/pdf_tiff/census2010.pdf"
    # gcs_source_uri = "gs://output_bucket-1/calcutta-may-dec1909.pdf"
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_gcp = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    # send the api request
    pages = [1]  # list of page#s, 5max for online / 2000max for offline/async
    requests = [{"input_config": input_gcp, "features": features, "pages": pages}]
    response = client.batch_annotate_files(requests)
    print(type(response))

    serialized = MessageToJson(response)
    print(type(serialized))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(serialized, f, ensure_ascii=False, indent=4)

    # for image_response in response.responses[0].responses:
    #     print(u"Full text: {}".format(image_response.full_text_annotation.text))
    #     for page in image_response.full_text_annotation.pages:
    #         for block in page.blocks:
    #             print(u"\nBlock confidence: {}".format(block.confidence))
    #             for par in block.paragraphs:
    #                 print(u"\tParagraph confidence: {}".format(par.confidence))
    #                 for word in par.words:
    #                     print(u"\t\tWord confidence: {}".format(word.confidence))
    #                     for symbol in word.symbols:
    #                         print(
    #                             u"\t\t\tSymbol: {}, (confidence: {})".format(
    #                                 symbol.text, symbol.confidence
    #                             )
    #                         )


if __name__ == '__main__':
    async_detect_document()
