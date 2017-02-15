cwlVersion: cwl:v1.0
class: CommandLineTool

requirements:
  - class: DockerRequirement
    dockerImageId: nlescsherlockdl/yolo:detect

baseCommand: [python, /scripts/run_yolo.py]
arguments: [--workflow_out, yolo.json]
inputs:
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
      glob: yolo.json
