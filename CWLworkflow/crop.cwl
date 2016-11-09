cwlVersion: cwl:draft-3
class: CommandLineTool
baseCommand: convert
inputs:
  - id: image_in
    type: File
    inputBinding:
      position: 1
  - id: crop_region
    type: string
    inputBinding:
      position: 2
      prefix: -crop
  - id: image_out
    type: string
    inputBinding:
      position: 3

outputs:
  - id: cropped_image
    type: File
    outputBinding:
      glob: $(inputs.image_out)

