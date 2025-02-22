# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""This module contains functions for obtaining JumpStart model packages."""
from __future__ import absolute_import
from typing import Optional
from sagemaker.jumpstart.constants import (
    JUMPSTART_DEFAULT_REGION_NAME,
)
from sagemaker.jumpstart.utils import (
    verify_model_region_and_return_specs,
)
from sagemaker.jumpstart.enums import (
    JumpStartScriptScope,
)


def _retrieve_model_package_arn(
    model_id: str,
    model_version: str,
    region: Optional[str],
    scope: Optional[str] = None,
    tolerate_vulnerable_model: bool = False,
    tolerate_deprecated_model: bool = False,
) -> Optional[str]:
    """Retrieves associated model pacakge arn for the model.

    Args:
        model_id (str): JumpStart model ID of the JumpStart model for which to
            retrieve the model package arn.
        model_version (str): Version of the JumpStart model for which to retrieve the
            model package arn.
        region (Optional[str]): Region for which to retrieve the model package arn.
        scope (Optional[str]): Scope for which to retrieve the model package arn.
        tolerate_vulnerable_model (bool): True if vulnerable versions of model
            specifications should be tolerated (exception not raised). If False, raises an
            exception if the script used by this version of the model has dependencies with known
            security vulnerabilities. (Default: False).
        tolerate_deprecated_model (bool): True if deprecated versions of model
            specifications should be tolerated (exception not raised). If False, raises
            an exception if the version of the model is deprecated. (Default: False).

    Returns:
        str: the model package arn to use for the model or None.
    """

    if region is None:
        region = JUMPSTART_DEFAULT_REGION_NAME

    model_specs = verify_model_region_and_return_specs(
        model_id=model_id,
        version=model_version,
        scope=scope,
        region=region,
        tolerate_vulnerable_model=tolerate_vulnerable_model,
        tolerate_deprecated_model=tolerate_deprecated_model,
    )

    if scope == JumpStartScriptScope.INFERENCE:

        if model_specs.hosting_model_package_arns is None:
            return None

        regional_arn = model_specs.hosting_model_package_arns.get(region)

        return regional_arn

    raise NotImplementedError(f"Model Package ARN not supported for scope: '{scope}'")
