def get_pipeline_summary(pipeline):

    """Generates list of dictionaries with setting summary for pipeline.

    Args:
        pipeline: Dictionary with pipeline setup (from .json file)

     Returns:
        pipeline_list: list of dictionaries with pipeline setup.
    """
    YES = '\u2713'
    NO = '\u2717'
    confounds = {"wm": "WM",
                 "csf": "CSF",
                 "gs": "GS",
                 "acompcor": "aCompCor",
                 "aroma": "ICA-Aroma",
                 "spikes": "Spikes"}

    pipeline_list = []

    for conf, conf_name in confounds.items():

        if conf != "aroma":
            if conf != "spikes":
                raw = YES if pipeline["confounds"][conf] else NO

                if not pipeline["confounds"][conf]:
                    temp_deriv = NO
                    quad_terms = NO

                if isinstance(pipeline["confounds"][conf], dict):

                    if pipeline["confounds"][conf]['temp_deriv']:
                        temp_deriv = YES

                    if pipeline["confounds"][conf]['quad_terms']:
                        quad_terms = NO

        if conf == "aroma":
            raw = YES if pipeline[conf] else NO
            temp_deriv = NO
            quad_terms = NO

        if conf == "spikes":
            raw = YES if pipeline[conf] else NO
            temp_deriv = NO
            quad_terms = NO

        pipeline_dict = {"Confound": conf_name,
                         "Raw": raw,
                         "Temp. deriv.": temp_deriv,
                         "Quadr. terms": quad_terms}

        pipeline_list.append(pipeline_dict)

    return(pipeline_list)


if __name__ == '__main__':
    import fmridenoise.utils.utils as ut
    from os.path import join, dirname
    pipeline = ut.load_pipeline_from_json(join(dirname(__file__), '..', 'pipelines', 'pipeline-36_parameters_gs.json'))
    summary = get_pipeline_summary(pipeline)
    print(summary)