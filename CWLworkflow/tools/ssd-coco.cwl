cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/ssd:detect-coco

baseCommand: /opt/detect_wrapper.py
inputs:
  workflow_out:
    type: string
    inputBinding:
      prefix: --workflow_out
      position: 1
  input_json:
    type: File
    inputBinding:
      position: 3
  input_directory:
    type: Directory
    inputBinding:
      prefix: --input_directory
      position: 2

outputs:
  json_out:
    type: File
    outputBinding:
      glob: $(inputs.workflow_out)
