# Gmail Add-on Prototype - Upwind Phishing Detector

This folder contains a Google Apps Script prototype for the Gmail add-on bonus requirement.

## Purpose

The add-on scans the currently opened Gmail message and displays phishing detection results directly inside the Gmail interface.

## Files

- `appsscript.json` - Google Apps Script manifest with Gmail add-on configuration.
- `Code.gs` - Add-on logic for reading the current Gmail message and detecting phishing indicators.

## Detection Indicators

The Gmail add-on checks for:

- IP addresses used in URLs
- Uncommon domains in URLs
- Possible spoofed sender addresses
- Urgent language such as `urgent`, `immediately`, and `action required`

## Notes

This is a safe local/prototype implementation designed for the official assignment bonus.
It does not scan external systems and does not perform any offensive activity.
