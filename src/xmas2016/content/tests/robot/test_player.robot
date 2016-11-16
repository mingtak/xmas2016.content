# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s xmas2016.content -t test_player.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src xmas2016.content.testing.XMAS2016_CONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_player.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Player
  Given a logged-in site administrator
    and an add player form
   When I type 'My Player' into the title field
    and I submit the form
   Then a player with the title 'My Player' has been created

Scenario: As a site administrator I can view a Player
  Given a logged-in site administrator
    and a player 'My Player'
   When I go to the player view
   Then I can see the player title 'My Player'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add player form
  Go To  ${PLONE_URL}/++add++Player

a player 'My Player'
  Create content  type=Player  id=my-player  title=My Player


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the player view
  Go To  ${PLONE_URL}/my-player
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a player with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the player title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
