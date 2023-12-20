from segment_anything import SamAutomaticMaskGenerator, sam_model_registry


def lambda_handler(event, context):
    print("Running!")
    sam = sam_model_registry["default"]
    mask_generator = SamAutomaticMaskGenerator(sam)
    print("Success!")
    #masks = mask_generator.generate(<your_image>)

