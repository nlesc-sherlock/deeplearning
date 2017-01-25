cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/list_directory

baseCommand: [python, /list_directory.py]
inputs:
  workflow_out:
    type: string
    inputBinding:
      prefix: --workflow_out
      position: 1
  input_files:
    type: Directory
    inputBinding:
      position: 2

outputs:
  json_out:
    type: File
    outputBinding:
      glob: $(inputs.workflow_out)
