cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerImageId: nlescsherlockdl/images_json

baseCommand: [/scripts/append_pipJson_with_visJson.py]
arguments: [--output_json, images_json.json]
inputs:
  json_input:
    type: File
    inputBinding:
      prefix: --input_json
      position: 1

outputs:
  json_out:
    type: File
    outputBinding:
      glob: images_json.json
