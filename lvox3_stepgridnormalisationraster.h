#ifndef LVOX3_STEPGRIDNORMALISATIONRASTER_H
#define LVOX3_STEPGRIDNORMALISATIONRASTER_H

#include "ct_step/abstract/ct_abstractstep.h"
#include "ct_tools/model/ct_autorenamemodels.h"

class LVOX3_StepGridNormalisationRaster : public CT_AbstractStep
{
    Q_OBJECT
public:

    LVOX3_StepGridNormalisationRaster(CT_StepInitializeData &dataInit);

    /**
     * @brief Return a short description of what do this class
     */
    QString getStepDescription() const;

    /*! \brief Step detailed description
     *
     * Return a detailed description of the step function
     */
    QString getStepDetailledDescription() const;

    /**
     * @brief Return a new empty instance of this class
     */
    CT_VirtualAbstractStep* createNewInstance(CT_StepInitializeData &dataInit);

protected:
    /**
     * @brief This method defines what kind of input the step can accept
     */
    void createInResultModelListProtected();

    /*! \brief Parameters DialogBox
     *
     * DialogBox asking for step parameters
     */
    void createPreConfigurationDialog();

    /**
     * @brief This method creates a window for the user to set the different parameters of the step.
     */
    void createPostConfigurationDialog();

    /**
     * @brief This method defines what kind of output the step produces
     */
    void createOutResultModelListProtected();

    /**
     * @brief This method do the job
     */
    void compute();
private:
    //QHash<QString, SumType> m_SumTypeCollection;
    //QHash<QString, GridType> _GridTypeCollection;
    QString _GridType;
    QString m_SumType;

    CT_AutoRenameModels _normalization_ModelName;
    CT_AutoRenameModels _normalization_group_ModelName;
};

#endif // LVOX3_STEPGRIDNORMALISATION_H
