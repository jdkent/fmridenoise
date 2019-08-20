from nipype.interfaces.base import SimpleInterface, BaseInterfaceInputSpec
from traits.trait_types import List, Dict, Directory
from fmridenoise.utils.report import create_report

class ReportCreatorInputSpec(BaseInterfaceInputSpec):
    pipelines = List(Dict(), mandatory=True)
    pipelines_names = List(Str(), mandatory=True)
    group_data_dir = Directory(exists=True)
    finished = Bool() # Placeholder
class ReportCreator(SimpleInterface):
    input_spec = ReportCreatorInputSpec

    def _run_interface(self, runtime):
        create_report(self.inputs.group_data_dir, self.inputs.pipelines)
        return runtime