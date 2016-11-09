cwlVersion: cwl:draft-3
class: CommandLineTool
baseCommand: ""
stdout: output.txt
hints:
  - class: DockerRequirement
    dockerPull: nlesc/imagenet1000
inputs:
  - id: image
    type: File
    inputBinding:
      position: 1
outputs:
  - id: output
    type: File
    outputBinding:
      glob: output.txt
