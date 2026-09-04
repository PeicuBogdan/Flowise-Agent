# Assembly Line 4 — Station Maintenance Manual

Document ID: MM-L4-018
Revision: 7
Applies to stations ST-01, ST-02 and ST-03.

---

## 1. Scope and structure

This manual covers first-line diagnostics for the three stations on Assembly
Line 4. It is written for maintenance technicians and line operators. Section 4
lists error codes, section 5 lists warning codes, and section 6 covers the
periodic maintenance schedule.

Repairs that require opening the drive cabinet or modifying robot programs are
outside the scope of this document and must be carried out by the automation
department.

---

## 2. Station overview

### ST-01 — UR10 Deburring Cell

A Universal Robots UR10 arm holding a pneumatic deburring spindle. Parts arrive
on a pallet conveyor, are clamped by a pneumatic fixture, deburred along a
programmed path, then released.

Nominal cycle time is 54 seconds. Cabinet temperature under normal load sits
between 38 and 46 degrees Celsius.

### ST-02 — Screwdriving Station

An automatic screwdriving unit with four spindles and a vibratory bowl feeder.
Torque is monitored per screw and logged to the line database. A part is
rejected if any of the four screws falls outside the torque window.

Nominal cycle time is 31 seconds. The station stops automatically after three
consecutive torque faults.

### ST-03 — Lubrication Station

A dosing unit that applies grease to two bearing seats per part. Grease is fed
from a 20 litre reservoir through a heated line. Dose volume is verified by a
flow meter on each shot.

Nominal cycle time is 68 seconds. The heated line runs between 55 and 65 degrees
Celsius.

---

## 3. Status values

The line monitoring system reports one of three states per station.

**running** — the station is executing its cycle normally. No operator action
required.

**warning** — the station is still producing, but a parameter has drifted
outside its normal band. Production continues. The warning must be cleared
before the end of the shift or it escalates to a stop.

**stopped** — the station has halted. An error code is always present when a
station is stopped. Production does not resume until the fault is acknowledged
and the cause removed.

---

## 4. Error codes

Error codes halt the station. The station reports status `stopped` and holds the
code until the fault is acknowledged on the HMI.

### E-101 — Emergency stop active

An emergency stop button on the station or on the line perimeter has been
pressed, or a safety gate is open.

Check every E-stop button on the station frame, the two perimeter buttons and
the gate interlock on the rear access door. Release the button by twisting it,
close the gate, then reset safety from the HMI. The station will not accept a
reset while any circuit is still open.

If the fault persists with all buttons released, the safety relay in the cabinet
has likely dropped out and needs the automation department.

### E-142 — Air pressure below minimum

Supply pressure has dropped below 5.5 bar. Pneumatic clamps and the deburring
spindle cannot operate safely below this value.

Read the gauge on the FRL unit at the station inlet. If pressure is low across
several stations, the fault is upstream at the compressor or the main line. If
it is low only here, check the inlet filter for blockage and inspect the supply
hose for leaks. A hissing sound near the clamp manifold usually means a failed
seal.

Acknowledge the error only after pressure is stable above 6 bar.

### E-233 — Screw torque out of tolerance

Three consecutive screws have been driven outside the configured torque window.
The station stops to avoid producing parts with unreliable joints. This code
applies to ST-02 only.

Common causes, in the order worth checking:

1. Empty or jammed bowl feeder. Look for screws bridging at the feed rail exit.
2. Worn bit. A rounded bit slips in the screw head and reads as low torque.
   Bits are consumable and should be replaced every 50,000 cycles.
3. Cross-threaded insert in the part. Inspect the last rejected part. If the
   thread is damaged, the problem is upstream, not at this station.
4. Drifted torque calibration. If the last three parts all read low by a similar
   margin, the spindle needs recalibration.

Remove the rejected part from the fixture before acknowledging. Do not clear
E-233 repeatedly without finding the cause; repeated clearing is the most common
reason bad joints reach the customer.

### E-310 — Robot protective stop

The UR10 has detected a force above its safety threshold and stopped. This code
applies to ST-01 only.

Usually a collision with a badly seated part, or a fixture that failed to clamp
before the path started. Inspect the tool and the part for damage, remove any
obstruction, then release the protective stop from the robot pendant before
resetting at the HMI.

Repeated protective stops on the same path segment suggest a fixture alignment
problem rather than a robot fault.

### E-407 — Dosing volume out of range

The flow meter measured a shot outside the accepted volume band. This code
applies to ST-03 only.

Check reservoir level first, then look for air in the feed line, which shows up
as inconsistent shot volumes rather than uniformly low ones. Bleed the line at
the purge valve until grease runs without bubbles. If the line temperature is
below 50 degrees, the grease is too viscous to dose accurately and the fault
will repeat until the heater recovers.

---

## 5. Warning codes

Warnings do not stop production. They must be resolved before the end of shift.

### W-107 — Cabinet temperature high

Cabinet temperature has exceeded 58 degrees Celsius. The station continues to
run, but drive electronics degrade above 70 degrees and the station will stop
with E-512 if temperature keeps climbing.

Check the cabinet filter mats first, they clog with grease mist and are the
cause in most cases. Confirm the cabinet fan is turning. Verify the cabinet door
is fully closed, since an open door disturbs the airflow path and makes cooling
worse rather than better.

On ST-03, also check whether the heated grease line is running above its
setpoint, as it adds heat directly into the enclosure.

### W-118 — Bit wear threshold reached

A screwdriving bit has passed 50,000 cycles. Production continues, but torque
scatter increases from this point and E-233 becomes more likely.

Replace the bit at the next changeover. Reset the counter on the HMI after
replacement, otherwise the warning reappears immediately.

### W-225 — Grease reservoir low

Reservoir level is below 15 percent. Roughly two hours of production remain at
nominal rate.

Refill with the grade specified on the station label. Mixing grades changes
viscosity and causes E-407 faults that look like a metering problem but are not.

---

## 6. Maintenance schedule

**Daily, per shift start**
Visual check for leaks, confirm air pressure above 6 bar, clear chips from
fixtures, confirm no active warnings on the HMI.

**Weekly**
Clean cabinet filter mats on all three stations. Check bit wear counter on
ST-02. Check grease reservoir level and top up if below 40 percent.

**Monthly**
Verify torque calibration on ST-02 against the reference transducer. Inspect
the UR10 tool mounting bolts on ST-01. Replace the inlet filter element on the
FRL units.

**Every 6 months**
Full torque recalibration on all four ST-02 spindles. Backup of robot programs
and station recipes. Inspection of the safety circuit including all E-stop
buttons and gate interlocks.

---

## 7. Escalation

Call the automation department when a fault involves the safety circuit, robot
programs, drive parameters or PLC logic. Call maintenance planning when the same
error code appears more than three times in one week, since that pattern points
to a wear problem rather than an incident.

Record every stop in the shift log with the station, the code and what was done.
The log is the only source for the weekly repeat-fault review.
