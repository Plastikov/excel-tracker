from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)

class Users(db.Model):
    __tablename__ = "users"
    UserId = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(255), unique=True, nullable=True)
    Lastname = db.Column(db.String(255), unique=True, nullable=True)
    Username = db.Column(db.String(255), unique=True, nullable=True)
    Password = db.Column(db.String(255), nullable=True)
    Email = db.Column(db.String(255), unique=True, nullable=True)
    Role = db.Column(db.String(50), nullable=True)
    Permissions = db.Column(db.String(255))
    IsEmailVerified = db.Column(db.Boolean, default=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"User(UserId={self.UserId}, Firstname='{self.Firstname}', Lastname='{self.Lastname}', Username='{self.Username}')"


class Children(db.Model):
    __tablename__ = "children"
    ChildId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey("users.UserId"), nullable=False)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    BirthDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Child(ChildId={self.ChildId}, FirstName='{self.FirstName}', LastName='{self.LastName}')"


class TrackingProfiles(db.Model):
    __tablename__ = "tracking_profiles"
    TrackingProfileId = db.Column(db.Integer, primary_key=True)
    ChildId = db.Column(db.Integer, db.ForeignKey("children.ChildId"), nullable=False)
    ProfileName = db.Column(db.String(255), nullable=False)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date)

    def __repr__(self):
        return f"TrackingProfile(TrackingProfileId={self.TrackingProfileId}, ProfileName='{self.ProfileName}')"


class Subjects(db.Model):
    __tablename__ = "subjects"
    SubjectId = db.Column(db.Integer, primary_key=True)
    SubjectName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)

    def __repr__(self):
        return f"Subject(SubjectId={self.SubjectId}, SubjectName='{self.SubjectName}')"


class Tools(db.Model):
    __tablename__ = "tools"
    ToolId = db.Column(db.Integer, primary_key=True)
    ToolName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)

    def __repr__(self):
        return f"Tool(ToolId={self.ToolId}, ToolName='{self.ToolName}')"


class SubjectTracking(db.Model):
    __tablename__ = "subject_tracking"
    SubjectTrackingId = db.Column(db.Integer, primary_key=True)
    TrackingProfileId = db.Column(
        db.Integer, db.ForeignKey("tracking_profiles.TrackingProfileId"), nullable=False
    )
    SubjectId = db.Column(
        db.Integer, db.ForeignKey("subjects.SubjectId"), nullable=False
    )

    def __repr__(self):
        return f"SubjectTracking(SubjectTrackingId={self.SubjectTrackingId}, TrackingProfileId={self.TrackingProfileId}, SubjectId={self.SubjectId})"


class ToolSubjectAssociation(db.Model):
    __tablename__ = "tool_subject_association"
    AssociationId = db.Column(db.Integer, primary_key=True)
    ToolId = db.Column(db.Integer, db.ForeignKey("tools.ToolId"), nullable=False)
    SubjectId = db.Column(
        db.Integer, db.ForeignKey("subjects.SubjectId"), nullable=False
    )

    def __repr__(self):
        return f"ToolSubjectAssociation(AssociationId={self.AssociationId}, ToolId={self.ToolId}, SubjectId={self.SubjectId})"


class AssessmentResults(db.Model):
    __tablename__ = "assessment_results"
    ResultId = db.Column(db.Integer, primary_key=True)
    ChildId = db.Column(db.Integer, db.ForeignKey("children.ChildId"), nullable=False)
    SubjectId = db.Column(
        db.Integer, db.ForeignKey("subjects.SubjectId"), nullable=False
    )
    ToolId = db.Column(db.Integer, db.ForeignKey("tools.ToolId"), nullable=False)
    ResultData = db.Column(db.Text)
    ResultDate = db.Column(db.Date)

    def __repr__(self):
        return f"AssessmentResults(ResultId={self.ResultId}, ChildId={self.ChildId}, SubjectId={self.SubjectId}, ToolId={self.ToolId})"


class Analytics(db.Model):
    __tablename__ = "analytics"
    AnalyticsId = db.Column(db.Integer, primary_key=True)
    ChildId = db.Column(db.Integer, db.ForeignKey("children.ChildId"), nullable=False)
    TrackingProfileId = db.Column(
        db.Integer, db.ForeignKey("tracking_profiles.TrackingProfileId"), nullable=False
    )
    AnalyticsData = db.Column(db.Text)
    AnalyticsDate = db.Column(db.Date)

    def __repr__(self):
        return f"Analytics(AnalyticsId={self.AnalyticsId}, ChildId={self.ChildId}, TrackingProfileId={self.TrackingProfileId})"

# models to be created:
# 1. user model to save the profile of all newly registered users
# 2. role model to identify the roles of different users
# 3. child model
# 4. tracking profile model will work under the child model to give \
# an overview of what is being tracked for each child
# 5. subject profile model will manage the subjects being tracked for each user
# 6. assessment model will track the tools been used for assessment, e.g say I
# have a tool called rote assessment that tracks the performance of a child
# in exercises whether done in class or home, class participation
