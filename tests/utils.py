import os
import math
import json
import shutil
import nipype as ni

def create_dummy_bids(root: str, subjetcts: int, sessions: int,        
                      derivatives: list=[], tasks: list=[],
                      *args: callable) -> None:  # TODO: Finish or delete
    subfill = math.floor(math.log10(subjetcts))+1
    if sessions != 0: 
        sesfill = math.floor(math.log10(sessions))+1
    os.makedirs(root, exist_ok=True)
    create_dummy_data_description(root)
    root_withderr = os.path.join(root, "derivatives")
    os.makedirs(root_withderr)
    create_dummy_data_description(root_withderr)
    for deriv in derivatives:
        deriv_path = os.path.join(root_withderr, deriv)
        os.makedirs(deriv_path)
        create_dummy_data_description(deriv_path)
        for sub_num in range(1, subjetcts+1):
            sub_path = os.path.join(deriv_path, f"sub-{str(sub_num).zfill(subfill)}")
            os.makedirs(sub_path)
            if sessions != 0:
                for ses_num in range(1, sessions+1):
                    ses_path = os.path.join(sub_path, f"ses-{str(ses_num).zfill(sesfill)}")
                    os.makedirs(ses_path)
                    try:
                        for func in args:
                            for task in tasks:
                                func(task, ses_path, sub_num, ses_num)
                    except:
                        import shutil
                        shutil.rmtree(root)
                        raise
            else:
                try:
                    for func in args:
                        for task in tasks:
                            func(task, sub_path, sub_num, 0)
                except:
                    import shutil
                    shutil.rmtree(root)
                    raise

def create_dummy_data_description(dir_path: str) -> None:
    """
    Creates dummy dataset_description.json in specified directory.
    
    Arguments:
        dir_path {str} -- path do destination directory

    Returns:
        None
    """
    data = """
{
    "Name": "Dummy Data",
    "BIDSVersion": "1.1.1",
    "PipelineDescription": {
        "Name": "DummyPipeline"
    }
}
    """
    with open(os.path.join(dir_path, "dataset_description.json"), 'w') as out:
        out.writelines(data)


def copy_as_dummy_dataset(source_bids_dir: str, new_path: str, ext_to_copy=tuple()) -> None:
    """
    Walks trough BIDS dataset and recreates it's structure but with
    empty files.
    
    Arguments:
        source_bids_dir {str} -- source of BIDS dataset
        new_path {str} -- destination of new dummy dataset
    
    Keyword Arguments:
        ext_to_copy {touple or str} -- files with given extensions
        will be copied insted of empty (default: {tuple()})
    
    Returns:
        None
    """

    if type(ext_to_copy) is str:
        ext_to_copy = (ext_to_copy,)
    source_bids_dir = os.path.abspath(source_bids_dir)
    os.makedirs(new_path)
    for root, dirs, files in os.walk(source_bids_dir, topdown=True):
        rel_root = os.path.relpath(root, source_bids_dir)
        rel_root = rel_root.strip(".")
        rel_root = rel_root.strip("/")
        new_root = os.path.join(new_path, rel_root)
        for name in dirs:
            os.makedirs(os.path.join(new_root, name))
        for name in files:
            for ext in ext_to_copy:
                if str(name).endswith(ext):
                    shutil.copy2(os.path.join(root, name), os.path.join(new_root, name))
                    break
            else:
                open(os.path.join(new_root, name), 'w').close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("bids_dir",
                        help="Data source bids directory.")
    parser.add_argument("target_directory",
                        help="Directory in which dummy dataset will be saved")
    parser.add_argument("-c", "--copy",
                        nargs="+",
                        default=['.json'],
                        help="Extensions of files that should be copied instead of creating dummy")
    args = parser.parse_args()
    copy_as_dummy_dataset(source_bids_dir=args.bids_dir,
                          new_path=args.target_directory,
                          ext_to_copy=args.copy)
