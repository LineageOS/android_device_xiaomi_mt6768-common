#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/mt6768-common',
    'hardware/mediatek',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.mediatek.hardware.videotelephony-V1-ndk'
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek',
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    'vendor/lib/hw/audio.primary.mt6768.so': blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v31.so'),
    'vendor/lib64/hw/fingerprint.mt6768.so': blob_fixup()
        .binary_regex_replace(
            b'\xc0\x03\x5f\xd6\x00\x00\x00\x00\xff\x03\x01\xd1\xfd\x7b\x02\xa9',
            b'\xc0\x03\x5f\xd6\x00\x00\x00\x00\xc0\x03\x5f\xd6\xfd\x7b\x02\xa9',
        ),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.13-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    (
        'vendor/lib64/libaalservice.so',
        'vendor/lib64/libcam.utils.sensorprovider.so',
        'librgbwlightsensor.so',
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/libgf_hal.so': blob_fixup()
        .binary_regex_replace(
            b'\x00\x14\xa0\x83\x5f\xb8\xfd\x7b\x43\xa9\xff\x03\x01\x91\xc0\x03\x5f\xd6\xff\x83\x01\xd1\xfd\x7b\x05\xa9\xfd\x43\x01\x91',
            b'\x00\x14\xa0\x83\x5f\xb8\xfd\x7b\x43\xa9\xff\x03\x01\x91\xc0\x03\x5f\xd6\x00\x00\xe0\xd2\xc0\x03\x5f\xd6\xfd\x43\x01\x91',
        ),
    'vendor/lib64/libmi_watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    (
        'vendor/lib64/libmtkcam_stdutils.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'mt6768-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
