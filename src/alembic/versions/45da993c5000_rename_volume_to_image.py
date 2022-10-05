"""rename volume to image

Revision ID: 45da993c5000
Revises: 3b1f69ed5bd9
Create Date: 2022-10-04 23:51:16.484340

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '45da993c5000'
down_revision = '3b1f69ed5bd9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.Column('transform', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sample_type', sa.String(), nullable=True),
    sa.Column('content_type', sa.String(), nullable=True),
    sa.Column('display_settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('dataset_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_name'], ['dataset.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_dataset_name'), 'image', ['dataset_name'], unique=False)
    op.create_index(op.f('ix_image_id'), 'image', ['id'], unique=False)
    op.create_index(op.f('ix_image_name'), 'image', ['name'], unique=False)
    op.create_table('view_to_image',
    sa.Column('view_id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['view_id'], ['view.id'], ),
    sa.PrimaryKeyConstraint('view_id', 'image_id')
    )
    op.create_index(op.f('ix_view_to_image_image_id'), 'view_to_image', ['image_id'], unique=False)
    op.create_index(op.f('ix_view_to_image_view_id'), 'view_to_image', ['view_id'], unique=False)
    op.drop_index('ix_volume_dataset_name', table_name='volume')
    op.drop_index('ix_volume_id', table_name='volume')
    op.drop_index('ix_volume_name', table_name='volume')
    op.drop_table('volume')
    op.drop_index('ix_view_to_volume_view_id', table_name='view_to_volume')
    op.drop_index('ix_view_to_volume_volume_id', table_name='view_to_volume')
    op.drop_table('view_to_volume')
    op.drop_constraint('crop_source_id_fkey', 'crop', type_='foreignkey')
    op.create_foreign_key(None, 'crop', 'image', ['source_id'], ['id'])
    op.add_column('mesh', sa.Column('image_id', sa.Integer(), nullable=True))
    op.drop_index('ix_mesh_volume_id', table_name='mesh')
    op.create_index(op.f('ix_mesh_image_id'), 'mesh', ['image_id'], unique=False)
    op.drop_constraint('mesh_volume_id_fkey', 'mesh', type_='foreignkey')
    op.create_foreign_key(None, 'mesh', 'image', ['image_id'], ['id'])
    op.drop_column('mesh', 'volume_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mesh', sa.Column('volume_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'mesh', type_='foreignkey')
    op.create_foreign_key('mesh_volume_id_fkey', 'mesh', 'volume', ['volume_id'], ['id'])
    op.drop_index(op.f('ix_mesh_image_id'), table_name='mesh')
    op.create_index('ix_mesh_volume_id', 'mesh', ['volume_id'], unique=False)
    op.drop_column('mesh', 'image_id')
    op.drop_constraint(None, 'crop', type_='foreignkey')
    op.create_foreign_key('crop_source_id_fkey', 'crop', 'volume', ['source_id'], ['id'])
    op.create_table('view_to_volume',
    sa.Column('view_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('volume_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['view_id'], ['view.id'], name='view_to_volume_view_id_fkey'),
    sa.ForeignKeyConstraint(['volume_id'], ['volume.id'], name='view_to_volume_volume_id_fkey'),
    sa.PrimaryKeyConstraint('view_id', 'volume_id', name='view_to_volume_pkey')
    )
    op.create_index('ix_view_to_volume_volume_id', 'view_to_volume', ['volume_id'], unique=False)
    op.create_index('ix_view_to_volume_view_id', 'view_to_volume', ['view_id'], unique=False)
    op.create_table('volume',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('format', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('transform', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sample_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('content_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('display_settings', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('dataset_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['dataset_name'], ['dataset.name'], name='volume_dataset_name_fkey'),
    sa.PrimaryKeyConstraint('id', name='volume_pkey')
    )
    op.create_index('ix_volume_name', 'volume', ['name'], unique=False)
    op.create_index('ix_volume_id', 'volume', ['id'], unique=False)
    op.create_index('ix_volume_dataset_name', 'volume', ['dataset_name'], unique=False)
    op.drop_index(op.f('ix_view_to_image_view_id'), table_name='view_to_image')
    op.drop_index(op.f('ix_view_to_image_image_id'), table_name='view_to_image')
    op.drop_table('view_to_image')
    op.drop_index(op.f('ix_image_name'), table_name='image')
    op.drop_index(op.f('ix_image_id'), table_name='image')
    op.drop_index(op.f('ix_image_dataset_name'), table_name='image')
    op.drop_table('image')
    # ### end Alembic commands ###
