#! /usr/bin/env python
#
#  freely taken from http://astroquery.readthedocs.org/en/latest/gallery.html
#
from astroquery.alma import Alma
from astroquery.splatalogue import Splatalogue
from astroquery.simbad import Simbad
from astropy import units as u
from astropy import constants
from spectral_cube import SpectralCube


m83table = Alma.query_object('M83', public=True)
m83urls = Alma.stage_data(m83table['Asdm_uid'])
# Sometimes there can be duplicates: avoid them with
# list(set())
m83files = Alma.download_and_extract_files(list(set(m83urls['URL'])))
m83files = list(set(m83files))

Simbad.add_votable_fields('rvel')
m83simbad = Simbad.query_object('M83')
rvel = m83simbad['RVel_Rvel'][0]*u.Unit(m83simbad['RVel_Rvel'].unit)

for fn in m83files:
    if 'line' in fn:
        cube = SpectralCube.read(fn)
        # Convert frequencies to their rest frequencies
        frange = u.Quantity([cube.spectral_axis.min(),
                             cube.spectral_axis.max()]) * (1+rvel/constants.c)

        # Query the top 20 most common species in the frequency range of the
        # cube with an upper energy state <= 50K
        lines = Splatalogue.query_lines(frange[0], frange[1], top20='top20',
                                        energy_max=50, energy_type='eu_k',
                                        only_NRAO_recommended=True)
        lines.pprint()

        # Change the cube coordinate system to be in velocity with respect
        # to the rest frequency (in the M83 rest frame)
        rest_frequency = lines['Freq-GHz'][0]*u.GHz / (1+rvel/constants.c)
        vcube = cube.with_spectral_unit(u.km/u.s,
                                        rest_value=rest_frequency,
                                        velocity_convention='radio')

        # Write the cube with the specified line name
        fmt = "{Species}{Resolved QNs}"
        row = lines[0]
        linename = fmt.format(**dict(zip(row.colnames,row.data)))
        vcube.write('M83_ALMA_{linename}.fits'.format(linename=linename))
