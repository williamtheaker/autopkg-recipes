#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Mostly stolen and modified from:
# https://github.com/autopkg/autopkg/blob/master/Code/autopkglib/MunkiOptionalReceiptEditor.py

import plistlib

from autopkglib import Processor, ProcessorError

__all__ = ["MunkiReceiptsDeleter"]


class MunkiReceiptsDeleter(Processor):
    """Deletes the receipts keys in a Munki pkginfo as specified."""

    input_variables = {
        "delete_all_receipts": {
            "required": True,
            "description": "Delete the entire receipts array.",
        },
        "pkg_ids": {
            "required": False,
            "description": "Array of receipt package IDs to delete.",
        },
        "pkginfo_repo_path": {
            "required": True,
            "description": "The repo path where the pkginfo was written.",
        },
    }
    output_variables = {}

    description = __doc__

    def main(self):
        if len(self.env["pkginfo_repo_path"]) < 1:
            raise ProcessorError("You must specify at least one pkginfo repo path")

        with open(self.env["pkginfo_repo_path"], "rb") as f:
            pkginfo = plistlib.load(f)

        receipts_deleted = False

        if "receipts" in pkginfo.keys():
            if self.env["delete_all_receipts"]:
                pkginfo.pop("receipts")
                self.output("Removing entire receipts array from pkginfo.")
                receipts_deleted = True
            else:
                for i, receipt in enumerate(pkginfo["receipts"]):
                    if receipt["packageid"] in self.env["pkg_ids"]:
                        pkginfo["receipts"].pop(i)
                        self.output(
                            f"Marking receipt {receipt['packageid']} for deletion"
                        )
                        receipts_deleted = True
        else:
            raise ProcessorError("pkginfo does not contain any receipts")

        if receipts_deleted:
            self.output(f"Writing updated pkginfo to {self.env['pkginfo_repo_path']}")
            with open(self.env["pkginfo_repo_path"], "wb") as f:
                plistlib.dump(pkginfo, f)
        else:
            self.output("No receipts modified, nothing to do")


if __name__ == "__main__":
    processor = MunkiReceiptsDeleter()
    processor.execute_shell()
