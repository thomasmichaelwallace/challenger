Challenger
==========
Challenges a LUSAS licence server until a licence is gained.

Check out http://www.beingbrunel.com/lusas-licence-challenger/ for more information.

Installing
----------

You can find a pre-built version of Challenger in the Releases section on [GitHub](https://github.com/thomasmichaelwallace/challenger/releases/download/v2.8/challenger-2-8.zip). Download, un-zip, configure (see next section) and run challenger.exe.

Note that you may need to download the Visual C++ 2010 re-distributable to use this pre-build version, you can find that on the [Microsoft Website](http://www.microsoft.com/en-gb/download/details.aspx?id=5555)

If you wish to build it; Challenger is a python script and therefore needs a python environment to run. As LUSAS is a Windows program, I would recommend investigating [PortablePython 3.2](http://www.portablepython.com/ "Portable Python"). Once installed Challenger can be run using __python challenger.exe__.

Configuration
-------------

Prior to the first run the __challenger.ini__ file will need to be updated to match your setup. Although the default values are sane, you ___must___ input your own LUSAS licence keys IDs. These are reported when you run the __lsmon.exe__ utility packaged with LUSAS, and are normally in the form LusasM_12345 for modeller, and LusasS_12345 for solver (where the digits are specific to your key).

Challenger will default to running LUSAS 14.7 from C:\LUSAS147. If you want to use a different version, or installation directory, you will can either update the ___paths___ section in the __challenger.ini__, or you can copy to:
	
	[DIRECTORY]\Third Party\Challenger

Where [DIRECTORY] is the root directory of the version of LUSAS you wish to use.

This has been tested on LUSAS 14.5, 14.6 and 14.7.

Author and Licence
==================

Challenger is primarily written by Thomas Michael Wallace (www.thomasmichaelwallace.co.uk), and released under the GPL v3 licence.
