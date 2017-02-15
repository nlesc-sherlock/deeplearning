cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/list_directory

baseCommand: [python, /list_directory.py]
arguments: [--workflow_out, files.json]
inputs:
  input_files:
    type: Directory
    inputBinding:
      position: 1

outputs:
  json_out:
    type: File
    outputBinding:
      glob: files.json
