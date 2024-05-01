

set -ex



python -m pip check
cd tests && pytest --cov arrow -k "not parse_tz_name_zzz"
exit 0
