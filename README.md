# Low-Cost Rubidium-Based Clock Reference

This project contains a hardware breakout board for an FE-5680A frequency reference, including a Python web UI to control the frequency offsets and monitor the PPS and Lock signal.

A detailed explanation is given in the publication proceedings of ISPCS 2026 (Low-Cost Rubidium-Based Clock Reference and Pulse-Per-Second Jitter Evaluation)

## Hardware

The hardware breakout board provides multiple decoupled 10 MHz outputs to allow for easy use in a laboratory environment. It also has a pulse per second output that is controllable in its pulse width.



## Software

The software stack allows for a simple control of the RFS via a Raspberry Pi. A USB to RS232 adapter that is connected to the RFS was utilized.


## License

This software is licensed under the Apache open-source license, while the hardware is under the CERN-OHL-W-2.0 open source license. Please refer to the license file in the `LICENSE` in the hardware and software directory.

We kindly ask all academic publications employing components of this work to cite the following paper:

For other licensing options please consult [Prof. Antonello Monti](mailto:amonti@eonerc.rwth-aachen.de).

## Contact


[![EONERC ACS Logo](./pictures/eonerc_logo.png)](http://www.acs.eonerc.rwth-aachen.de)

- Manuel Pitz <manuel.pitz@eonerc.rwth-aachen.de>
- Sebastian Uerlich <sebastian.uerlich@eonerc.rwth-aachen.de>
- Benish Khan <benish.khan@eonerc.rwth-aachen.de>
- Leonid Kalinin <leonid.kalinin@rwth-aachen.de>



[Institute for Automation of Complex Power Systems (ACS)](http://www.acs.eonerc.rwth-aachen.de)
[EON Energy Research Center (EONERC)](http://www.eonerc.rwth-aachen.de)
[RWTH University Aachen, Germany](http://www.rwth-aachen.de)

## Acknowledgment

This research has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101172829. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or CINEA. Neither the European Union nor the granting authority can be held responsible for them.

We are grateful for the financial support of the [BMWE (Federal Ministry of Economic Affairs and Energy)](https://www.bundeswirtschaftsministerium.de/Navigation/EN/Home/home.html), funding reference [03EI6125A](https://www.enargus.de/pub/bscw.cgi/?op=enargus.eps2&q=beaver&v=10&id=243841191).

<img src="./pictures/BMWE_gefoerdert_en_RGB.png" alt="drawing" width="200"/>