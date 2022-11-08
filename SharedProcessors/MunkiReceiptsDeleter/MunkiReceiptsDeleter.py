#!/usr/bin/env python

import plistlib

from autopkglib import Processor, ProcessorError

__all__ = ["MunkiReceiptsDeleter"]


class MunkiReceiptsDeleter(Processor):
    """Modifies the receipts key in a Munki pkginfo."""

    input_variables = {
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

        receipts_deleted = []
        if "receipts" in pkginfo.keys():
            for i, receipt in enumerate(pkginfo["receipts"]):
                # made optional any pkginfos
                if receipt["packageid"] in self.env["delete_receipts"]:
                    pkginfo["receipts"][i] = None
                    self.output(
                        f"Setting package ID {receipt['packageid']} as optional"
                    )
                    receipts_deleted.append(receipt["packageid"])
        else:
            raise ProcessorError("pkginfo does not contain any receipts")

        if len(receipts_deleted) > 0:
            self.output(f"Writing pkginfo to {self.env['pkginfo_repo_path']}")
            with open(self.env["pkginfo_repo_path"], "wb") as f:
                plistlib.dump(pkginfo, f)
        else:
            self.output("No receipts modified, nothing to do")


if __name__ == "__main__":
    processor = MunkiReceiptsDeleter()
    processor.execute_shell()