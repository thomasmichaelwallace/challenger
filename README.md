Challenger
==========
Challenges a LUSAS licence server until a licence is gained.

Check out http://www.beingbrunel.com/lusas-licence-challenger/ for more information.

Installing
----------

Challenger is a python script and therefore needs a python environment to run. As LUSAS is a Windows program, I would reccomend investigating PortablePython 3.2.

Prior to the first run the configuration varaibles at the top of the script need to be changed to match your setup; especially the licence key ID.

Challenger will default to running LUSAS 14.7 from C:\LUSAS147. If you want to use a different version, or installation directoy, you will need to copy Challenger.exe to:
	
	[DIRECTORY]\Third Party\Challenger\Challenger.exe

Where [DIRECTORY] is the root directory of the version of LUSAS you wish to use.

This has been tested on LUSAS 14.5, 14.6 and 14.7.

Author and Licence
==================

Challenger is primiarly written by Thomas Michael Wallace (www.thomasmichaelwallace.co.uk), and released under the GPL v3 licence.
