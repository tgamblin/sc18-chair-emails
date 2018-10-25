# SC18 session chair emails

This repo has some scripts to build emails with ICS attachments for SC18
session chairs.

## Inputs:
* `chairs.txt`: tab-separated session_id / name / email for each chair
* `sess*.ics` files: calendar invitations for each session from the
[SC18 tech papers program](https://sc18.supercomputing.org/program/papers/)

## Ouputs:
* `sess*.eml`: emails to session chairs generated from the session ->
  chair mapping and each calendar invitation.

## Requirements:
* This requires Python 3.
* You'll need to pip3 install -r requirements.txt to use it.  This gets
  you the `ics` package for reading calendars.
