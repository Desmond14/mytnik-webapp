import play.Project._

name := "mytnik"

version := "1.0-SNAPSHOT"

libraryDependencies ++= Seq(
  javaJdbc,
  javaEbean,
  cache,
  javaJpa,
  "org.hibernate" % "hibernate-entitymanager" % "3.6.9.Final"
)     

libraryDependencies += "net.sourceforge.jtds" % "jtds" % "1.3.1"

playJavaSettings
