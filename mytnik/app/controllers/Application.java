package controllers;

import models.Manifest;
import play.db.jpa.Transactional;
import play.mvc.Controller;
import play.mvc.Result;

import java.util.List;

public class Application extends Controller {

    public static Result GO_HOME = redirect(
            routes.Application.displayHomepage()
    );

    public static Result index() {
        return GO_HOME;
    }

    public static Result displayHomepage() {
        return ok(views.html.index.render());
    }

    @Transactional
    public static Result mapManifestsView() {
        List<Manifest> results = Manifest.selectAllManifests();
        return ok(views.html.manifest.render(results));
    }

}
