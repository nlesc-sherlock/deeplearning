cwlVersion: cwl:v1.0
class: CommandLineTool

requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/upload

baseCommand: [python, /scripts/upload.py]
inputs:
  json_input:
    type: File
    inputBinding:
      prefix: --json_input
      position: 1
  directories:
    type: 
      type: array
      items: Directory
      inputBinding:
        prefix: --directory
  filename:
    type: string
    inputBinding:
      prefix: --filename
  user:
    type: string
    inputBinding:
      prefix: --webdav-user
  password:
    type: string
    inputBinding:
      prefix: --webdav-password
  url:
    type: string
    inputBinding:
      prefix: --webdav-url

outputs:
  url: string

stdout: cwl.output.json
    
