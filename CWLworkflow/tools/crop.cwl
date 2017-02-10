cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/cropper

baseCommand: [python, /scripts/crop.py]
inputs:
  json_input_file:
    type: File
    inputBinding:
      prefix: --json_input_file
      position: 1
  workflow_out:
    type: string
    inputBinding:
      prefix: --workflow_out
      position: 2
  input_directory:
    type: Directory
    inputBinding:
      prefix: --input_directory
      position: 3
  probability:
    type: float
    inputBinding:
      prefix: --probability
      position: 5
  cropped_folder:
    type: string
    inputBinding:
      prefix: --cropped_folder
      position: 4
  specialised:
    type: boolean?
    inputBinding:
      prefix: --specialised
      position: 6
  verbose:
    type: boolean?
    inputBinding:
      prefix: -v
      position: 7

outputs:                                                                                                                                 
  json_out:
    type: File
    outputBinding:
      glob: $(inputs.workflow_out)
  cropped_out:
    type: Directory
    outputBinding:
      glob: "cropped"

