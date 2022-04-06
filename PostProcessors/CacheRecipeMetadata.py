#!/usr/bin/python
#
# Based originally on LastRecipeRunResult
# Copyright 2019-Present Graham R Pugh
# Copyright 2022 Gusto, Inc. (https://www.gusto.com/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for CacheRecipeMetadata class"""

from datetime import datetime
import os.path
import json

from autopkglib import Processor  # pylint: disable=import-error


__all__ = ["CacheRecipeMetadata"]


class CacheRecipeMetadata(Processor):
    """An AutoPkg processor for writing recipe metadata to a JSON file."""

    input_variables = {
        "output_file_path": {"description": ("Path to output file."), "required": False},
        "output_file_name": {
            "description": ("Name of output file."),
            "required": False,
            "default": "autopkg_metadata.json",
        },
        "url": {"description": ("the download URL."), "required": False},
        "RECIPE_PATH": {"description": ("The name of the package."), "required": False},
        "pathname": {
            "description": ("The path to the downloaded installer."),
            "required": False,
        },
        "last_modified": {
            "description": ("last_modified output from URLDownloader."),
            "required": False,
        },
        "etag": {
            "description": ("etag output from URLDownloader."),
            "required": False,
            "default": None,
        },
    }

    output_variables = {
        "url": {"description": ("the download URL.")},
        "last_modified": {"description": ("The current package last_modified.")},
        "etag": {"description": ("The outputted value for etag.")},
        "RECIPE_PATH": {"description": ("the package name.")},
    }

    description = __doc__

    def get_latest_recipe_run_info(self, output_file):
        """Load CacheRecipeMetadata output from disk."""
        try:
            with open(output_file, "r") as fp:
                data = json.load(fp)
        except (IOError, ValueError):
            data = {}
        return data

    def main(self):
        """output the values to a file in the location provided"""

        output_file_path = self.env.get("output_file_path")
        output_file_name = self.env.get("output_file_name")
        pathname = self.env.get("pathname")
        recipe_name = self.env.get("RECIPE_PATH")
        url = self.env.get("url")
        last_modified = self.env.get("last_modified")
        etag = self.env.get("etag")

        recipe_path, recipe_filename = os.path.split(recipe_name)

        if url:
            self.output("URL: {}".format(url))

        if not output_file_path:
            output_file_path = "/tmp"
        output_file = os.path.join(output_file_path, output_file_name)

        # Load stored JSON file
        data = self.get_latest_recipe_run_info(output_file)

        cache_modified = False

        # Replace modified values
        # Create new key if recipe metadata not previously cached
        if recipe_filename not in data.keys():
            data[recipe_filename] = {}

        data[recipe_filename]["url"] = url

        if pathname:
            self.output("Path: {}".format(pathname))
            data[recipe_filename]["pathname"] = pathname

        if etag:
            self.output("etag: {}".format(etag))
            cache_modified = True
            data[recipe_filename]["etag"] = etag
        if last_modified:
            self.output("last_modified: {}".format(last_modified))
            cache_modified = True
            data[recipe_filename]["last_modified"] = last_modified
        if cache_modified:
            data[recipe_filename]["cache_timestamp"] = str(datetime.now())

        # Write changes back to stored JSON file
        with open(output_file, "w") as outfile:
            json.dump(data, outfile)

        self.output(f"Metadata cache written to: {output_file}")


if __name__ == "__main__":
    PROCESSOR = CacheRecipeMetadata()
    PROCESSOR.execute_shell()
