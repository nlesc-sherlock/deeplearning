cwlVersion: cwl:draft-3
class: Workflow
inputs:
  - id: image_in
    type: File
  - id: crop_region
    type: string
  - id: image_out
    type: string
outputs:
  - id: output
    type: File
    source: "#classify/output"
steps:
  - id: crop
    run: crop.cwl
    inputs:
      - id: image_in
        source: "#image_in"
      - id: crop_region
        source: "#crop_region"
      - id: image_out
        source: "#image_out"
    outputs:
      - id: cropped_image
        
  - id: classify
    run: classify_image.cwl
    inputs:
      - id: image
        source: "#crop/cropped_image"
    outputs:
      - id: output

