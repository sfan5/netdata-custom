import React from "react"
import { Button } from "@netdata/netdata-ui"
import Tooltip from "@/src/components/tooltips"

import { useHttp } from "hooks/use-http"

const NETDATA_LATEST_VERSION_URL = "https://api.github.com/repos/netdata/netdata/releases/latest"
const NETDATA_LATEST_GCS_VERSION_URL =
  "https://www.googleapis.com/storage/v1/b/netdata-nightlies/o/latest-version.txt"

const transformGcsVersionResponse = data => data.replace(/(\r\n|\n|\r| |\t)/gm, "")

const transformGithubResponse = data => data?.tag_name.replace(/(\r\n|\n|\r| |\t)/gm, "")

const versionsMatch = (v1, v2) => {
  if (v1 === v2) {
    return true
  }
  let s1 = v1.split(".")
  let s2 = v2.split(".")
  // Check major version
  let n1 = parseInt(s1[0].substring(1, 2), 10)
  let n2 = parseInt(s2[0].substring(1, 2), 10)
  if (n1 < n2) return false
  if (n1 > n2) return true

  // Check minor version
  n1 = parseInt(s1[1], 10)
  n2 = parseInt(s2[1], 10)
  if (n1 < n2) return false
  if (n1 > n2) return true

  // Split patch: format could be e.g. 0-22-nightly
  s1 = s1[2].split("-")
  s2 = s2[2].split("-")

  n1 = parseInt(s1[0], 10)
  n2 = parseInt(s2[0], 10)
  if (n1 < n2) return false
  if (n1 > n2) return true

  n1 = s1.length > 1 ? parseInt(s1[1], 10) : 0
  n2 = s2.length > 1 ? parseInt(s2[1], 10) : 0
  if (n1 < n2) return false
  return true
}

const VersionControl = ({ currentVersion, releaseChannel }) => {
  return null
}

export default VersionControl
