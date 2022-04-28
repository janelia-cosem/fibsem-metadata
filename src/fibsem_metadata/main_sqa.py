from sqlalchemy.orm import Session
from fibsem_metadata.database_sqa import create_db_and_tables, engine
import fibsem_metadata.schemas.views as schemas
from fibsem_metadata.models.manifest import DatasetManifest
import json

def ingest_dataset(path):
    with open(path) as fh:
        blob = json.load(fh)
    dmeta = DatasetManifest(**blob)
    
    # generate the acquisition table
    acq_model = dmeta.metadata.imaging
    sample_model = dmeta.metadata.sample
       
    acq_table = schemas.FIBSEMAcquisition(instrument="",
                                        institution=acq_model.institution,
                                        start_date=acq_model.startDate,
                                        sampling_grid_unit='nm',
                                        sampling_grid_spacing=acq_model.gridSpacing.values.values(),
                                        sampling_grid_shape=[10,10,10],
                                        duration_days=acq_model.duration,
                                        bias_voltage=acq_model.biasVoltage,
                                        scan_rate=acq_model.scanRate,
                                        current=acq_model.current,
                                        primary_energy=acq_model.primaryEnergy)
    
    sample_table = schemas.Sample(organism=sample_model.organism,
                                  type=sample_model.type,
                                  substype=sample_model.subtype,
                                  treatment=sample_model.treatment,
                                  contributions=sample_model.contributions)

    pub_tables = [schemas.Publication(name=d.title, url=d.href) for d in dmeta.metadata.DOI]
    pub_tables.extend([schemas.Publication(name=d.title, url=d.href) for d in dmeta.metadata.publications])

    dataset = schemas.Dataset(name=dmeta.metadata.id,
                              description=dmeta.metadata.title,
                              institution=dmeta.metadata.institution,
                              software_availability=dmeta.metadata.softwareAvailability,
                              acquisition_id = acq_table.id,
                              sample_id = sample_table.id,
                              publications=pub_tables)

    volume_tables = []
    for key, value in dmeta.sources.items():
        volume_tables.append(schemas.Volume(name=value.name, 
                                            description=value.description,
                                            url=value.url,
                                            format=value.format,
                                            transform=value.transform,
                                            sample_type=value.sampleType,
                                            content_type=value.contentType,
                                            dataset_id=dataset.id,
                                            ))

    return acq_table, sample_table, pub_tables, dataset, volume_tables



if __name__ == '__main__':
    create_db_and_tables(engine, wipe=True)
    with Session(engine) as session:
        table = ingest_dataset('api/jrc_hela-2/manifest.json')
        session.add_all([table])
        session.commit()

