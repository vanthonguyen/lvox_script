#include "lvox3_stepgridnormalisationraster.h"

//In/Out dependencies
#include "ct_result/model/inModel/ct_inresultmodelgrouptocopy.h"
#include "ct_result/model/outModel/tools/ct_outresultmodelgrouptocopypossibilities.h"
#include "ct_result/ct_resultgroup.h"
#include "ct_itemdrawable/ct_scene.h"
#include "ct_itemdrawable/ct_image2d.h"
#include "tools/lvox3_gridtype.h"


//Tools dependencies
#include "ct_view/ct_stepconfigurabledialog.h"
// point cloud
#define DEF_SearchInResult      "rs"
#define DEF_SearchInGroup       "gs"
#define DEF_SearchInGrid        "gr"

#define DEF_SearchInDTMGridResult      "dr"
#define DEF_SearchInDTMGridGroup       "dg"
#define DEF_SearchInDTMGrid            "gdt"

LVOX3_StepGridNormalisationRaster::LVOX3_StepGridNormalisationRaster(CT_StepInitializeData &dataInit) : CT_AbstractStep(dataInit)
{

}

QString LVOX3_StepGridNormalisationRaster::getStepDescription() const
{
    return tr("Normalisation des hauteur d'une grille par dtm en format raster 2D (en developpement)");
}

// Step detailed description
QString LVOX3_StepGridNormalisationRaster::getStepDetailledDescription() const
{
    return tr("Cette étape permet diminuer la hauteur des voxel d'une grille selon un roster de hauteur. "
              "À noter que les paramètres devraient être les mêmes pour la grille 3D importée et les grilles 3D calculées présentement pour empêcher des résultats incohérents. (résolution de grille et dimension)");
}

CT_VirtualAbstractStep* LVOX3_StepGridNormalisationRaster::createNewInstance(CT_StepInitializeData &dataInit)
{
    // Creates an instance of this step
    return new LVOX3_StepGridNormalisationRaster(dataInit);
}

void LVOX3_StepGridNormalisationRaster::createPreConfigurationDialog()
{

}

void LVOX3_StepGridNormalisationRaster::createInResultModelListProtected()
{
    CT_InResultModelGroupToCopy *resultModel = createNewInResultModelForCopy(DEF_SearchInResult, tr("Grids"), "", true);
  	resultModel->setZeroOrMoreRootGroup();
    resultModel->addGroupModel("", DEF_SearchInGroup, CT_AbstractItemGroup::staticGetType(), tr("Group"));
    resultModel->addItemModel(DEF_SearchInGroup, DEF_SearchInGrid, LVOX3_AbstractGrid3D::staticGetType(), tr("Grid to be normalized"));

    //DTM
    CT_InResultModelGroupToCopy *resultDtm = createNewInResultModelForCopy(DEF_SearchInDTMGridResult, tr("Raster de modèle numérique de terrain (geotiff)"), "", true);
    resultDtm->setZeroOrMoreRootGroup();
    resultDtm->addGroupModel("", DEF_SearchInDTMGridGroup, CT_AbstractItemGroup::staticGetType(), tr("Groupe de dtm"), "");
    resultDtm->addItemModel(DEF_SearchInDTMGridGroup, DEF_SearchInDTMGrid, CT_Image2D<float>::staticGetType(), tr("DTM"));

}


void LVOX3_StepGridNormalisationRaster::createPostConfigurationDialog()
{

}

void LVOX3_StepGridNormalisationRaster::createOutResultModelListProtected()
{
    CT_OutResultModelGroupToCopyPossibilities* res = createNewOutResultModelToCopy(DEF_SearchInResult);
    std::cout<<DEF_SearchInResult<<std::endl;
    if(res != nullptr){
        res->addItemModel(DEF_SearchInGroup, _normalization_ModelName, new lvox::Grid3Df(), tr("Flatted Grid"));
    }
}

void LVOX3_StepGridNormalisationRaster::compute()
{
    //QList<CT_ResultGroup*> outResult =
    CT_ResultGroup* resultOutGrids = getOutResultList().first();

    CT_ResultGroupIterator itGrp(resultOutGrids, this, DEF_SearchInGroup);

    CT_ResultGroup* dtmResult = getInputResults().at(1);

    CT_ResultGroupIterator itDtmGrp(dtmResult, this, DEF_SearchInDTMGridGroup);
    while(itGrp.hasNext() && itDtmGrp.hasNext() && !isStopped()) {
        /*
         * Two casts are required, the group iterator returns const objects and
         * because addItemDrawable() is called, it has to be non const.
         */
        CT_StandardItemGroup *group = dynamic_cast<CT_StandardItemGroup*>((CT_AbstractItemGroup*)itGrp.next());
        lvox::Grid3Df* inGrid = dynamic_cast<lvox::Grid3Df*> (group->firstItemByINModelName(this, DEF_SearchInGrid));

        CT_StandardItemGroup *dtmGroup = dynamic_cast<CT_StandardItemGroup*>((CT_AbstractItemGroup*)itDtmGrp.next());
        CT_Image2D<float>* dtm = (CT_Image2D<float>*)dtmGroup->firstItemByINModelName(this, DEF_SearchInDTMGrid);

        float xres = inGrid->xresolution();
        float yres = inGrid->yresolution();
        float zres = inGrid->zresolution();
        float NAd = 0;

        size_t xdim = inGrid->xdim();
        size_t ydim = inGrid->ydim();
        size_t zdim = inGrid->zdim();


        lvox::Grid3Df* itemoutiConteur = (lvox::Grid3Df*) inGrid->copy(_normalization_ModelName.completeName(), resultOutGrids, CT_ResultCopyModeList());


        group->addItemDrawable(itemoutiConteur);

        //all voxel in dtm have the same z coordinate !!!
        double coordZ = dtm->valueAtIndexAsDouble(0);
        double minZ = inGrid->minZ();
        double minDtmZ = std::numeric_limits<double>::max();
        //std::vector<bool> isNotEmptyColumns(xdim*ydim, false);
        for(size_t xx = 0; xx < xdim; xx++)
        {
            for(size_t yy = 0; yy < ydim; yy++)
            {
                //nombre de voxels
                //int nbValeur = div(MNT->valueAtCoords(xx,yy),zres).quot;
                //find first non null
                double coordX = inGrid->getCellCenterX(xx);
                double coordY = inGrid->getCellCenterY(yy);
                float dtmZ = dtm->valueAtCoords(coordX, coordY);

//                size_t minZIndex = 0;
//                inGrid->index(xx, yy, 0, minZIndex);
                //double minZ = inGrid->valueAtIndexAsDouble(minZIndex);
                //compute the number of voxel must be descended
                bool isNotEmptyColumn = false;

                for(size_t zz = 0; zz < zdim; zz++)
                {
                    size_t index = 0;
                    inGrid->index(xx, yy, zz, index);
                    if (inGrid->valueAtIndexAsDouble(index) >= 0){
                        isNotEmptyColumn = true;
                        break;
                    }
                }
                int diff = (dtmZ - minZ)/zres;
                if(diff > 0 && isNotEmptyColumn){
                    if( dtmZ < minDtmZ ){
                        minDtmZ = dtmZ;
                    }
                }
            }
        }

        //correction of height
        for(size_t xx = 0; xx < xdim; xx++)
        {
            for(size_t yy = 0; yy < ydim; yy++)
            {
                double coordX = inGrid->getCellCenterX(xx);
                double coordY = inGrid->getCellCenterY(yy);
                float dtmZ = dtm->valueAtCoords(coordX, coordY);

                size_t minZIndex = 0;
                inGrid->index(xx, yy, 0, minZIndex);
                //double minZ = inGrid->valueAtIndexAsDouble(minZIndex);
                //compute the number of voxel must be descended
                int beginZlevel = (minDtmZ - minZ)/zres;
                int diff = (dtmZ - minDtmZ)/zres;
                //qDebug()<<"###diff"<< diff<< "minZ" << minZ << "dtmZ"<< dtmZ << "minDtm" << minDtmZ;
                if(diff > 0){
                    for(size_t zz = beginZlevel + diff; zz < zdim; zz++)
                    {
                        size_t index = 0;
                        inGrid->index(xx, yy, zz, index);
                        float currentValue = inGrid->valueAtIndexAsDouble(index);
                        itemoutiConteur->setValue(xx, yy, zz - diff, currentValue);
                        if( zdim - zz >= diff){
                            itemoutiConteur->setValue(xx, yy, zz, -1);
                        }
                    }
                }
            }
        }

        itemoutiConteur->computeMinMax();
    }
}
