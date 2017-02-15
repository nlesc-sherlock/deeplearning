cwlVersion: cwl:v1.0
class: CommandLineTool

cwl:requirements:
  - class: DockerRequirement
    dockerPull: nlescsherlockdl/cropper

baseCommand: [python, /scripts/crop.py]
arguments: [--workflow_out, cropped.json, --cropped_folder, cropped]
inputs:
  json_input_file:
    type: File
    inputBinding:
      prefix: --json_input_file
      position: 1
  input_directory:
    type: Directory
    inputBinding:
      prefix: --input_directory
      position: 2
  probability:
    type: float
    inputBinding:
      prefix: --probability
      position: 3
  specialised:
    type: boolean?
    inputBinding:
      prefix: --specialised
      position: 4
  verbose:
    type: boolean?
    inputBinding:
      prefix: -v
      position: 5

outputs:                                                                                                                                 
  json_out:
    type: File
    outputBinding:
      glob: cropped.json
  cropped_out:
    type: Directory
    outputBinding:
      glob: cropped

