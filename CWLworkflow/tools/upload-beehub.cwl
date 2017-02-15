cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/upload

baseCommand: [python, /scripts/upload.py]
inputs:
  input_json:
    type: File
    inputBinding:
      prefix: --json_input
      position: 1
  input_files:
    type: Directory
    inputBinding:
      prefix: --input_directory
      position: 2
  filename:
    type: string
    inputBinding:
      prefix: --filename
      position: 3
  user:
    type: string
    inputBinding:
      prefix: --webdav-user
      position: 4
  password:
    type: string
    inputBinding:
      prefix: --webdav-password
      position: 5
  url:
    type: string
    inputBinding:
      prefix: --webdav-url
      position: 6

outputs:
  url: string

stdout: cwl.output.json
    
