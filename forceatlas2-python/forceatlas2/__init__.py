import os, pkg_resources
import pandas as pd
from subprocess import check_call

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # < Python 3.8: Use backport module
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version('forceatlas2-python')
    del version
except PackageNotFoundError:
    pass


def forceatlas2(file_name, target_change_per_node=0, target_steps=100, is3d=True, n_jobs = 4, memory = "8"):
    output_coord_file = "{file_name}.coords.txt".format(file_name=file_name)

    classpath = (
            pkg_resources.resource_filename("forceatlas2", "ext/forceatlas2.jar")
            + ":"
            + pkg_resources.resource_filename("forceatlas2", "ext/gephi-toolkit-0.9.2-all.jar")
    )

    command = [
            "java",
            "-Djava.awt.headless=true",
            "-Xmx{memory}g".format(memory=memory),
            "-cp",
            classpath,
            "kco.forceatlas2.Main",
            "--input",
            file_name,
            "--output",
            file_name + ".coords",
            "--nthreads",
            str(n_jobs),
            "--targetChangePerNode",
            str(target_change_per_node),
            "--targetSteps",
            str(target_steps),
            "--nsteps",
            str(100),
    ]
    if not is3d:
        command.append("--2d")

    check_call(command)

    fle_coords = pd.read_csv(output_coord_file, header=0, index_col=0, sep="\t").values
    #os.remove(output_coord_file)

    return fle_coords
