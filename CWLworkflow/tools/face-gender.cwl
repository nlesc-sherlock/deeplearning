cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerImageId: nlescsherlockdl/face:gender-wrapper

baseCommand: [/scripts/image_classify_workflow_wrap_gender.py, --json]
arguments: [--workflow_out, gender.json]
inputs:
  json_input:
    type: File
    inputBinding:
      position: 2
  input_directory:
    type: Directory
    inputBinding:
      prefix: -D
      position: 1
  

outputs:
  json_out:
    type: File
    outputBinding:
      glob: gender.json
