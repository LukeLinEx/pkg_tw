from taiwanese.back.utils.gmail import *
from taiwanese.back.student_list import HandleStudentList
from taiwanese.back.utils.drive import GDrive
from taiwanese.back.utils.doc import GDoc
from taiwanese.config import *

hsl = HandleStudentList()
drive = GDrive()
doc = GDoc()

with open("./email_template") as f:
    email_template = f.read()


def hw_notification(week, sender="luke.lin@taany.org", subject="台語課作業"):
    try:
        [r for r in drive.list_files(material_g_folder_id) if r["name"]==week][0]["id"]
    except IndexError:
        raise ValueError("The content for the week doesn't exist")

    for student_id, name, email in hsl.active[1:]:
        ref = "https://lukelandwalker.com/homework/{}/{}/".format(week, student_id)
        ref = "<a href='{}'>This</a>".format(ref)

        msg = email_template.format(name, ref, week)
        msg = create_message(sender, email, subject, msg)
        send_message("me", msg)


if __name__ == "__main__":
    hw_notification("20210111")

