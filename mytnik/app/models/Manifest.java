package models;

import play.db.jpa.JPA;

import javax.persistence.Entity;
import javax.persistence.Id;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by kklimek on 2014-04-12.
 */
@Entity
public class Manifest {

    @Id
    public String messageId;
    public String unbReference;
    public String sentDate;
    public String eta;
    public String sender;
    public String originalSender;
    public String vesselName;
    public String voyageNumber;
    public String terminal;
    public Integer containersCount;
    public Integer plFull;
    public Integer plEmpty;
    public Integer transhipment;

    public static List<Manifest> selectAllManifests() {
        @SuppressWarnings("unchecked")
        List<Object[]> allManifests = JPA.em().createNativeQuery("SELECT MessageId, UnbReference, DocumentCreationTime, ArrivalTime, SenderId, OriginalSenderId, VesselName, VoyageNumber, RecipientId from ent.ve_Message").getResultList();
        @SuppressWarnings("unchecked")
        List<Object[]> allManifestsStats = JPA.em().createNativeQuery("SELECT ContainerCount, PlFullCount, PlEmptyCount, TranshipmentCount from ent.ve_MessageContainerStatistics").getResultList();

        List<Manifest> res = new ArrayList<Manifest>();
        for (int i = 0; i < allManifests.size(); ++i) {
            Manifest manifest = new Manifest();
            manifest.messageId = String.valueOf(allManifests.get(i)[0]);
            manifest.unbReference = String.valueOf(allManifests.get(i)[1]);
            manifest.sentDate = String.valueOf(allManifests.get(i)[2]);
            manifest.eta = String.valueOf(allManifests.get(i)[3]);
            manifest.sender = String.valueOf(allManifests.get(i)[4]);
            manifest.originalSender = String.valueOf(allManifests.get(i)[5]);
            manifest.vesselName = String.valueOf(allManifests.get(i)[6]);
            manifest.voyageNumber = String.valueOf(allManifests.get(i)[7]);
            manifest.terminal = String.valueOf(allManifests.get(i)[8]);
            manifest.containersCount = (Integer) allManifestsStats.get(i)[0];
            manifest.plFull = (Integer) allManifestsStats.get(i)[1];
            manifest.plEmpty = (Integer) allManifestsStats.get(i)[2];
            manifest.transhipment = (Integer) allManifestsStats.get(i)[3];
            res.add(manifest);
        }
        return res;
    }
}
