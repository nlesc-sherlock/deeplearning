cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/face:detector-minimal-wrapper

baseCommand: /scripts/face_detection_workflow_wrap.py --json
inputs:
  workflow_out:
    type: string
    inputBinding:
      prefix: --workflow_out
      position: 1
  json_input:
    type: File
    inputBinding:
      position: 3
  input_directory:
    type: Directory
    inputBinding:
      prefix: -D
      position: 2
  

outputs:
  json_out:
    type: File
    outputBinding:
      glob: $(inputs.workflow_out)