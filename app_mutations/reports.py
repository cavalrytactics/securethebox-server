import graphene
from app_models.models import Report
from app_types.types import ReportType

class ReportInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateReportMutation(graphene.Mutation):
    report = graphene.Field(ReportType)
    class Arguments:
        report_data = ReportInput(required=True)
    def mutate(self, info, report_data=None):
        report = Report(
            value=report_data.value
        )
        report.save()
        return CreateReportMutation(report=report)

class UpdateReportMutation(graphene.Mutation):
    report = graphene.Field(ReportType)
    class Arguments:
        report_data = ReportInput(required=True)
    @staticmethod
    def get_object(ID):
        return Report.objects.get(pk=ID)
    def mutate(self, info, report_data=None):
        report = UpdateReportMutation.get_object(report_data.ID)
        if report_data.value:
            report.value = report_data.value
        report.save()
        return UpdateReportMutation(report=report)

class DeleteReportMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Report.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteReportMutation(success=success)