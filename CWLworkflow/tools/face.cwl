cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerImageId: nlescsherlockdl/face:detector-wrapper

baseCommand: [/scripts/face_detection_workflow_wrap.py, --json]
arguments: [--workflow_out, face.json]
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
      glob: face.json
